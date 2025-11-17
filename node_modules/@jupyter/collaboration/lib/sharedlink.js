// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Dialog, showDialog } from '@jupyterlab/apputils';
import { PageConfig, URLExt } from '@jupyterlab/coreutils';
import { nullTranslator } from '@jupyterlab/translation';
import { Widget } from '@lumino/widgets';
/**
 * Show the shared link dialog
 *
 * @param options Shared link dialog options
 * @returns Dialog result
 */
export async function showSharedLinkDialog({ translator }) {
    const trans = (translator !== null && translator !== void 0 ? translator : nullTranslator).load('collaboration');
    const token = PageConfig.getToken();
    const url = new URL(URLExt.normalize(PageConfig.getUrl({
        workspace: PageConfig.defaultWorkspace
    })));
    return showDialog({
        title: trans.__('Share Jupyter Server Link'),
        body: new SharedLinkBody(url.toString(), token, PageConfig.getOption('hubUser') !== '', trans),
        buttons: [
            Dialog.cancelButton(),
            Dialog.okButton({
                label: trans.__('Copy Link'),
                caption: trans.__('Copy the link to the Jupyter Server')
            })
        ]
    });
}
class SharedLinkBody extends Widget {
    constructor(_url, _token, _behindHub, _trans) {
        super();
        this._url = _url;
        this._token = _token;
        this._behindHub = _behindHub;
        this._trans = _trans;
        this._tokenCheckbox = null;
        this.onTokenChange = (e) => {
            const target = e.target;
            this.updateContent(target === null || target === void 0 ? void 0 : target.checked);
        };
        this._warning = document.createElement('div');
        this.populateBody(this.node);
        this.addClass('jp-shared-link-body');
    }
    /**
     * Returns the input value.
     */
    getValue() {
        var _a;
        const withToken = ((_a = this._tokenCheckbox) === null || _a === void 0 ? void 0 : _a.checked) === true;
        if (withToken) {
            const url_ = new URL(this._url);
            url_.searchParams.set('token', this._token);
            return url_.toString();
        }
        else {
            return this._url;
        }
    }
    onAfterAttach(msg) {
        var _a;
        super.onAfterAttach(msg);
        (_a = this._tokenCheckbox) === null || _a === void 0 ? void 0 : _a.addEventListener('change', this.onTokenChange);
    }
    onBeforeDetach(msg) {
        var _a;
        (_a = this._tokenCheckbox) === null || _a === void 0 ? void 0 : _a.removeEventListener('change', this.onTokenChange);
        super.onBeforeDetach(msg);
    }
    updateContent(withToken) {
        this._warning.innerHTML = '';
        const urlInput = this.node.querySelector('input[readonly]');
        if (withToken) {
            if (urlInput) {
                const url_ = new URL(this._url);
                url_.searchParams.set('token', this._token.slice(0, 5));
                urlInput.value = url_.toString() + '…';
            }
            this._warning.appendChild(document.createElement('h3')).textContent =
                this._trans.__('Security warning!');
            this._warning.insertAdjacentText('beforeend', this._trans.__('Anyone with this link has full access to your notebook server, including all your files!'));
            this._warning.insertAdjacentHTML('beforeend', '<br>');
            this._warning.insertAdjacentText('beforeend', this._trans.__('Please be careful who you share it with.'));
            this._warning.insertAdjacentHTML('beforeend', '<br>');
            if (this._behindHub) {
                this._warning.insertAdjacentText('beforeend', // You can restart the server to revoke the token in a JupyterHub
                this._trans.__('They will be able to access this server AS YOU.'));
                this._warning.insertAdjacentHTML('beforeend', '<br>');
                this._warning.insertAdjacentText('beforeend', this._trans.__('To revoke access, go to File -> Hub Control Panel, and restart your server.'));
            }
            else {
                this._warning.insertAdjacentText('beforeend', 
                // Elsewhere, you *must* shut down your server - no way to revoke it
                this._trans.__('Currently, there is no way to revoke access other than shutting down your server.'));
            }
        }
        else {
            if (urlInput) {
                urlInput.value = this._url;
            }
            if (this._behindHub) {
                this._warning.insertAdjacentText('beforeend', this._trans.__('Only users with `access:servers` permissions for this server will be able to use this link.'));
            }
            else {
                this._warning.insertAdjacentText('beforeend', this._trans.__('Only authenticated users will be able to use this link.'));
            }
        }
    }
    populateBody(dialogBody) {
        dialogBody.insertAdjacentHTML('afterbegin', `<input readonly value="${this._url}">`);
        if (this._token) {
            const label = dialogBody.appendChild(document.createElement('label'));
            label.insertAdjacentHTML('beforeend', '<input type="checkbox">');
            this._tokenCheckbox = label.firstChild;
            label.insertAdjacentText('beforeend', this._trans.__('Include token in URL'));
            dialogBody.insertAdjacentElement('beforeend', this._warning);
            this.updateContent(false);
        }
    }
}
