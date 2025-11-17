import { Contents } from '@jupyterlab/services';
/**
 * Document session model
 */
export interface ISessionModel {
    /**
     * Document format; 'text', 'base64',...
     */
    format: Contents.FileFormat;
    /**
     * Document type
     */
    type: Contents.ContentType;
    /**
     * File unique identifier
     */
    fileId: string;
    /**
     * Server session identifier
     */
    sessionId: string;
}
export declare function requestDocSession(format: string, type: string, path: string): Promise<ISessionModel>;
