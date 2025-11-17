import { Dialog } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
/**
 * Shared link dialog options
 */
export interface ISharedLinkDialogOptions {
    /**
     * Translation object.
     */
    translator?: ITranslator | null;
}
/**
 * Show the shared link dialog
 *
 * @param options Shared link dialog options
 * @returns Dialog result
 */
export declare function showSharedLinkDialog({ translator }: ISharedLinkDialogOptions): Promise<Dialog.IResult<string>>;
