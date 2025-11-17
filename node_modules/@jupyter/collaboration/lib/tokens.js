// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import { Token } from '@lumino/coreutils';
/**
 * The user menu token.
 *
 * NOTE: Require this token in your extension to access the user menu
 * (top-right menu in JupyterLab's interface).
 */
export const IUserMenu = new Token('@jupyter/collaboration:IUserMenu');
/**
 * The global awareness token.
 */
export const IGlobalAwareness = new Token('@jupyter/collaboration:IGlobalAwareness');
