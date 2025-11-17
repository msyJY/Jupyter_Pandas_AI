import * as React from 'react';
import { Awareness } from 'y-protocols/awareness';
import { Panel } from '@lumino/widgets';
import { ReactWidget } from '@jupyterlab/apputils';
import { User } from '@jupyterlab/services';
import { ICollaboratorAwareness } from './tokens';
export declare class CollaboratorsPanel extends Panel {
    private _currentUser;
    private _awareness;
    private _body;
    constructor(currentUser: User.IManager, awareness: Awareness, fileopener: (path: string) => void);
    /**
     * Handle collaborator change.
     */
    private _onAwarenessChanged;
}
/**
 * The collaborators list.
 */
export declare class CollaboratorsBody extends ReactWidget {
    private _collaborators;
    private _fileopener;
    constructor(fileopener: (path: string) => void);
    get collaborators(): ICollaboratorAwareness[];
    set collaborators(value: ICollaboratorAwareness[]);
    render(): React.ReactElement<any>[];
}
