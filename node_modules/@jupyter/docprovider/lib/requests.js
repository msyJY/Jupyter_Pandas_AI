/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
/**
 * Document session endpoint provided by `jupyter_collaboration`
 * See https://github.com/jupyterlab/jupyter_collaboration
 */
const DOC_SESSION_URL = 'api/collaboration/session';
export async function requestDocSession(format, type, path) {
    const settings = ServerConnection.makeSettings();
    const url = URLExt.join(settings.baseUrl, DOC_SESSION_URL, encodeURIComponent(path));
    const body = {
        method: 'PUT',
        body: JSON.stringify({ format, type })
    };
    let response;
    try {
        response = await ServerConnection.makeRequest(url, body, settings);
    }
    catch (error) {
        throw new ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}
