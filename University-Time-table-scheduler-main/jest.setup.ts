import '@testing-library/jest-dom'
import 'whatwg-fetch'
import { TextEncoder, TextDecoder } from 'util'

// Polyfills for TextEncoder and TextDecoder
global.TextEncoder = TextEncoder as any
global.TextDecoder = TextDecoder as any

// Mock BroadcastChannel for Jest tests since it's not available
globalThis.BroadcastChannel = globalThis.BroadcastChannel || class {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
  postMessage() {}
  close() {}
  addEventListener() {}
  removeEventListener() {}
  dispatchEvent() { return true; }
};

// Simple polyfills for streams
globalThis.WritableStream = globalThis.WritableStream || class {
  constructor() {}
  getWriter() {
    return {
      write: () => Promise.resolve(),
      close: () => Promise.resolve(),
      abort: () => Promise.resolve(),
    };
  }
};

globalThis.TransformStream = globalThis.TransformStream || class {
  constructor() {
    this.readable = {
      getReader: () => ({
        read: () => Promise.resolve({ done: true, value: undefined }),
        releaseLock: () => {},
      }),
    };
    this.writable = {
      getWriter: () => ({
        write: () => Promise.resolve(),
        close: () => Promise.resolve(),
        abort: () => Promise.resolve(),
      }),
    };
  }
};

// Polyfill for MSW headers issue with jsdom
Object.defineProperty(window, 'Headers', {
  writable: true,
  value: class extends window.Headers {
    append(name: string, value: string) {
      if (name.toLowerCase() === 'x-interceptors-internal-request-id') return;
      super.append(name, value);
    }
    set(name: string, value: string) {
      if (name.toLowerCase() === 'x-interceptors-internal-request-id') return;
      super.set(name, value);
    }
  }
});
 