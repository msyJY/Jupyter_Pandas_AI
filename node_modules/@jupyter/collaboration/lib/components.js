// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
import * as React from 'react';
/**
 * React component for the user icon.
 *
 * @returns The React component
 */
export const UserIconComponent = props => {
    const { user } = props;
    return (React.createElement("div", { className: "jp-UserInfo-Container" },
        React.createElement("div", { title: user.display_name, className: "jp-UserInfo-Icon", style: { backgroundColor: user.color } },
            React.createElement("span", null, user.initials)),
        React.createElement("h3", null, user.display_name)));
};
