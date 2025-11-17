import { Extension } from '@codemirror/state';
import { Awareness } from 'y-protocols/awareness';
import { Text } from 'yjs';
/**
 * Yjs document objects
 */
export type EditorAwareness = {
    /**
     * User related information
     */
    awareness: Awareness;
    /**
     * Shared editor source
     */
    ytext: Text;
};
/**
 * CodeMirror extension to display remote users cursors
 *
 * @param config Editor source and awareness
 * @returns CodeMirror extension
 */
export declare function remoteUserCursors(config: EditorAwareness): Extension;
