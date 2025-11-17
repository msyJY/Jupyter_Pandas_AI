// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { TableOfContentsFactory } from '@jupyterlab/toc';
/**
 * Base table of contents model factory for file editor
 */
export class EditorTableOfContentsFactory extends TableOfContentsFactory {
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    createNew(widget, configuration) {
        const model = super.createNew(widget, configuration);
        const onActiveHeadingChanged = (model, heading) => {
            if (heading) {
                widget.content.editor.setCursorPosition({
                    line: heading.line,
                    column: 0
                });
            }
        };
        model.activeHeadingChanged.connect(onActiveHeadingChanged);
        widget.disposed.connect(() => {
            model.activeHeadingChanged.disconnect(onActiveHeadingChanged);
        });
        return model;
    }
}
//# sourceMappingURL=factory.js.map