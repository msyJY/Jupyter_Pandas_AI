import { User } from '@jupyterlab/services';
import { Menu, MenuBar } from '@lumino/widgets';
import { VirtualElement } from '@lumino/virtualdom';
/**
 * Custom renderer for the user menu.
 */
export declare class RendererUserMenu extends MenuBar.Renderer {
    private _user;
    /**
     * Constructor of the class RendererUserMenu.
     *
     * @argument user Current user object.
     */
    constructor(user: User.IManager);
    /**
     * Render the virtual element for a menu bar item.
     *
     * @param data - The data to use for rendering the item.
     *
     * @returns A virtual element representing the item.
     */
    renderItem(data: MenuBar.IRenderData): VirtualElement;
    /**
     * Render the label element for a menu item.
     *
     * @param data - The data to use for rendering the label.
     *
     * @returns A virtual element representing the item label.
     */
    renderLabel(data: MenuBar.IRenderData): VirtualElement;
    /**
     * Render the user icon element for a menu item.
     *
     * @returns A virtual element representing the item label.
     */
    private _createUserIcon;
}
/**
 * This menu does not contain anything but we keep it around in case someone uses it.
 * Custom lumino Menu for the user menu.
 */
export declare class UserMenu extends Menu {
    constructor(options: UserMenu.IOptions);
}
/**
 * Namespace of the UserMenu class.
 */
export declare namespace UserMenu {
    /**
     * User menu options interface
     */
    interface IOptions extends Menu.IOptions {
        /**
         * Current user manager.
         */
        user: User.IManager;
    }
}
