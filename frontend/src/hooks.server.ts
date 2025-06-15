import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);
  
  // Allow PDF files to be embedded in iframes
  if (event.url.pathname.endsWith('.pdf')) {
    response.headers.delete('X-Frame-Options');
    response.headers.set('Content-Security-Policy', 'frame-ancestors \'self\'');
  }
  
  return response;
};