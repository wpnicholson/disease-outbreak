export function once<T extends Event>(fn: ((event: T) => void) | null): (event: T) => void {
    return function (this: unknown, event: T) {
        if (fn) fn.call(this, event);
        fn = null;
    };
}
export function preventDefault<T extends Event>(fn: (event: T) => void): (event: T) => void {
    return function (this: unknown, event: T) {
        event.preventDefault();
        fn.call(this, event);
    };
}
