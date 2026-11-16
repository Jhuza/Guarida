import { useSyncExternalStore } from 'react';
const empty = Object.freeze({ mood: 'disponible', status: 'Exploración libre', chat: [], ai_enabled: false, remaining: 0 });
let snapshot = empty;
const subscribers = new Set();
function receive(event) {
  if (event.source !== window.parent || event.data?.type !== 'streamlit:render') return;
  const next = { ...empty, ...event.data.args };
  if (JSON.stringify(next.chat) === JSON.stringify(snapshot.chat)) next.chat = snapshot.chat;
  snapshot = next;
  for (const notify of subscribers) notify();
}
window.addEventListener('message', receive);
export function post(type, data = {}) {
  window.parent.postMessage({ isStreamlitMessage: true, type, ...data }, '*');
}
export function sendAction(action, data = {}) {
  const id = crypto.randomUUID();
  post('streamlit:setComponentValue', { value: { id, action, ...data }, dataType: 'json' });
  return id;
}
export function useServer() {
  return useSyncExternalStore(listener => { subscribers.add(listener); return () => subscribers.delete(listener); }, () => snapshot, () => empty);
}
export function ready() { post('streamlit:componentReady', { apiVersion: 1 }); }
