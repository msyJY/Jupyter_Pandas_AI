import { TranslationBundle } from '@jupyterlab/translation';
import { Contents, Drive, User } from '@jupyterlab/services';
import { ICollaborativeDrive, ISharedModelFactory } from './tokens';
/**
 * A Collaborative implementation for an `IDrive`, talking to the
 * server using the Jupyter REST API and a WebSocket connection.
 */
export declare class YDrive extends Drive implements ICollaborativeDrive {
    /**
     * Construct a new drive object.
     *
     * @param user - The user manager to add the identity to the awareness of documents.
     */
    constructor(user: User.IManager, translator: TranslationBundle);
    /**
     * SharedModel factory for the YDrive.
     */
    readonly sharedModelFactory: ISharedModelFactory;
    /**
     * Dispose of the resources held by the manager.
     */
    dispose(): void;
    /**
     * Get a file or directory.
     *
     * @param localPath: The path to the file.
     *
     * @param options: The options used to fetch the file.
     *
     * @returns A promise which resolves with the file content.
     *
     * Uses the [Jupyter Notebook API](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/jupyter/notebook/master/notebook/services/api/api.yaml#!/contents) and validates the response model.
     */
    get(localPath: string, options?: Contents.IFetchOptions): Promise<Contents.IModel>;
    /**
     * Save a file.
     *
     * @param localPath - The desired file path.
     *
     * @param options - Optional overrides to the model.
     *
     * @returns A promise which resolves with the file content model when the
     *   file is saved.
     */
    save(localPath: string, options?: Partial<Contents.IModel>): Promise<Contents.IModel>;
    private _onCreate;
    private _user;
    private _trans;
    private _providers;
}
