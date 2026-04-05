import { useEffect } from 'react';

export default function useModal(isOpen, onClose) {
  useEffect(() => {
    if (!isOpen) return;
    const onEsc = (e) => e.key === 'Escape' && onClose();
    window.addEventListener('keydown', onEsc);
    return () => window.removeEventListener('keydown', onEsc);
  }, [isOpen, onClose]);
}
