async function req(path, method = 'GET', body) {
  const res = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined
  });
  return res.json();
}

export const api = {
  auth: (action, payload) => req(`/api/auth?action=${action}`, 'POST', payload),
  admin: (action, payload) => req(`/api/admin?action=${action}`, 'POST', payload),
  requests: (action, payload) => req(`/api/requests?action=${action}`, 'POST', payload),
  reports: (action, payload) => req(`/api/reports?action=${action}`, 'POST', payload),
  settings: (action, payload) => req(`/api/settings?action=${action}`, 'POST', payload),
  sync: (action, payload) => req(`/api/sync?action=${action}`, 'POST', payload)
};
