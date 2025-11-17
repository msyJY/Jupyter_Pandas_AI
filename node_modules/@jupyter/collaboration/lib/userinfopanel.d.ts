import { ReactWidget } from '@jupyterlab/apputils';
import { User } from '@jupyterlab/services';
import { Panel } from '@lumino/widgets';
export declare class UserInfoPanel extends Panel {
    private _profile;
    private _body;
    constructor(user: User.IManager);
}
/**
 * A SettingsWidget for the user.
 */
export declare class UserInfoBody extends ReactWidget {
    private _user;
    /**
     * Constructs a new settings widget.
     */
    constructor(user: User.IIdentity);
    get user(): User.IIdentity;
    set user(user: User.IIdentity);
    render(): JSX.Element;
}
