/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { showErrorMessage, Dialog } from '@jupyterlab/apputils';
import { PromiseDelegate } from '@lumino/coreutils';
import { Signal } from '@lumino/signaling';
import { WebsocketProvider as YWebsocketProvider } from 'y-websocket';
import { requestDocSession } from './requests';
/**
 * A class to provide Yjs synchronization over WebSocket.
 *
 * We specify custom messages that the server can interpret. For reference please look in yjs_ws_server.
 *
 */
export class WebSocketProvider {
    /**
     * Construct a new WebSocketProvider
     *
     * @param options The instantiation options for a WebSocketProvider
     */
    constructor(options) {
        this._onConnectionClosed = (event) => {
            if (event.code === 1003) {
                console.error('Document provider closed:', event.reason);
                showErrorMessage(this._trans.__('Document session error'), event.reason, [
                    Dialog.okButton()
                ]);
                // Dispose shared model immediately. Better break the document model,
                // than overriding data on disk.
                this._sharedModel.dispose();
            }
        };
        this._onSync = (isSynced) => {
            var _a;
            if (isSynced) {
                this._ready.resolve();
                (_a = this._yWebsocketProvider) === null || _a === void 0 ? void 0 : _a.off('sync', this._onSync);
            }
        };
        this._ready = new PromiseDelegate();
        this._isDisposed = false;
        this._path = options.path;
        this._contentType = options.contentType;
        this._format = options.format;
        this._serverUrl = options.url;
        this._sharedModel = options.model;
        this._awareness = options.model.awareness;
        this._yWebsocketProvider = null;
        this._trans = options.translator;
        const user = options.user;
        user.ready
            .then(() => {
            this._onUserChanged(user);
        })
            .catch(e => console.error(e));
        user.userChanged.connect(this._onUserChanged, this);
        this._connect().catch(e => console.warn(e));
    }
    /**
     * Test whether the object has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise that resolves when the document provider is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Dispose of the resources held by the object.
     */
    dispose() {
        var _a, _b, _c;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        (_a = this._yWebsocketProvider) === null || _a === void 0 ? void 0 : _a.off('connection-close', this._onConnectionClosed);
        (_b = this._yWebsocketProvider) === null || _b === void 0 ? void 0 : _b.off('sync', this._onSync);
        (_c = this._yWebsocketProvider) === null || _c === void 0 ? void 0 : _c.destroy();
        Signal.clearData(this);
    }
    async _connect() {
        const session = await requestDocSession(this._format, this._contentType, this._path);
        this._yWebsocketProvider = new YWebsocketProvider(this._serverUrl, `${session.format}:${session.type}:${session.fileId}`, this._sharedModel.ydoc, {
            disableBc: true,
            params: { sessionId: session.sessionId },
            awareness: this._awareness
        });
        this._yWebsocketProvider.on('sync', this._onSync);
        this._yWebsocketProvider.on('connection-close', this._onConnectionClosed);
    }
    _onUserChanged(user) {
        this._awareness.setLocalStateField('user', user.identity);
    }
}
