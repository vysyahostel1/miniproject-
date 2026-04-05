export const showToast = (text, type = 'success') => {
  window.dispatchEvent(new CustomEvent('ifrh-toast', { detail: { text, type } }));
};
