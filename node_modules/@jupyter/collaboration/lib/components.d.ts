import { User } from '@jupyterlab/services';
import * as React from 'react';
type Props = {
    user: User.IIdentity;
};
/**
 * React component for the user icon.
 *
 * @returns The React component
 */
export declare const UserIconComponent: React.FC<Props>;
export {};
