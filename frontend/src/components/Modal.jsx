import React from 'react'

export default function Modal({ open, onClose, children }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-lg max-w-2xl w-full relative">
        <button className="absolute top-2 right-2 text-xl" onClick={onClose}>×</button>
        {children}
      </div>
    </div>
  )
}