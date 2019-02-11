/**
 * This file contains type declarations and HTTP request helper functions
 */

export type HTTPResponse = SuccessResponse<any> | FailureResponse;

export interface SuccessResponse<T> {
    status: 'SUCCESS';
    data: T;
}

export type FailureResponse = {
    status: 'FAILURE',
    data: { message: string },
};

export const failureResponse = (message: string): FailureResponse => ({
    status: 'FAILURE',
    data: { message: message }
});

export const successResponse = <T>(data: T): SuccessResponse<T> => ({
    status: 'SUCCESS',
    data: data
});

export const isFailureResponse = (arg: HTTPResponse): arg is FailureResponse => arg.status === 'FAILURE';

export const GETRequest = async (url: string): Promise<HTTPResponse> => {
    const response = await fetch(url, {method: 'GET'});

    if (response.status !== 200) {
        return handleResponseError(response.status);
    }

    try {
        return await response.json();
    } catch (err) {
        return failureResponse("Failure occurred when making GET request: " + err);
    }
};

export const POSTRequest = async (url: string, payload: object): Promise<HTTPResponse> => {

    const response = await fetch(url,
        {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

    if (response.status !== 200) {
        return handleResponseError(response.status);
    }

    // Try to send a json response if appropriate. If there is no JSON to be returned, just send a success code
    try {
        return await response.json();
    } catch (err) {
        return successResponse(200);
    }
};

/**
 * Returns a rejected promise with a message catered for the given error code
 * @param {number} status: An HTTP error status code
 * @returns {Promise<never>}
 */
const handleResponseError = (status: number) => {
    switch (status) {
        case 400:
            return Promise.reject("Bad Request: 400");
        case 401:
            return Promise.reject("Not authenticated: 401");
        case 403:
            return Promise.reject("Insufficient privileges: 403");
        case 404:
            return Promise.reject("Resource not found: 404");
        case 500:
            return Promise.reject("Server error: 500");
        default:
            return Promise.reject("Error occurred: " + status);
    }
};