import { DocumentRegistry, IDocumentWidget } from '@jupyterlab/docregistry';
import { TableOfContents, TableOfContentsModel } from '@jupyterlab/toc';
import { Widget } from '@lumino/widgets';
import { FileEditor } from '../widget';
import { EditorTableOfContentsFactory, IEditorHeading } from './factory';
/**
 * Table of content model for LaTeX files.
 */
export declare class LaTeXTableOfContentsModel extends TableOfContentsModel<IEditorHeading, IDocumentWidget<FileEditor, DocumentRegistry.IModel>> {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType(): string;
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions(): (keyof TableOfContents.IConfig)[];
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    protected getHeadings(): Promise<IEditorHeading[] | null>;
}
/**
 * Table of content model factory for LaTeX files.
 */
export declare class LaTeXTableOfContentsFactory extends EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget: Widget): boolean;
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    protected _createNew(widget: IDocumentWidget<FileEditor, DocumentRegistry.IModel>, configuration?: TableOfContents.IConfig): LaTeXTableOfContentsModel;
}
