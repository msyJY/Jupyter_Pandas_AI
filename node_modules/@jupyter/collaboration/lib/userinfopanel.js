// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { ReactWidget } from '@jupyterlab/apputils';
import { Panel } from '@lumino/widgets';
import * as React from 'react';
import { UserIconComponent } from './components';
export class UserInfoPanel extends Panel {
    constructor(user) {
        super({});
        this.addClass('jp-UserInfoPanel');
        this._profile = user;
        this._body = null;
        if (this._profile.isReady) {
            this._body = new UserInfoBody(this._profile.identity);
            this.addWidget(this._body);
            this.update();
        }
        else {
            this._profile.ready
                .then(() => {
                this._body = new UserInfoBody(this._profile.identity);
                this.addWidget(this._body);
                this.update();
            })
                .catch(e => console.error(e));
        }
    }
}
/**
 * A SettingsWidget for the user.
 */
export class UserInfoBody extends ReactWidget {
    /**
     * Constructs a new settings widget.
     */
    constructor(user) {
        super();
        this._user = user;
    }
    get user() {
        return this._user;
    }
    set user(user) {
        this._user = user;
        this.update();
    }
    render() {
        return React.createElement(UserIconComponent, { user: this._user });
    }
}
