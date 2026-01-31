import React from 'react';

export default function NoteCard({ note, onDecrypt, onEdit, onDelete, isDecrypted, decryptedContent }) {
  const formatDate = (timestamp) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <p className="text-xs text-gray-500">{formatDate(note.created_at)}</p>
          <p className="text-sm text-gray-400 break-all mt-2">
            {isDecrypted ? decryptedContent : `Encrypted: ${note.cipher_text.substring(0, 50)}...`}
          </p>
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        {!isDecrypted && (
          <button
            onClick={() => onDecrypt(note.id)}
            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 transition text-sm"
          >
            Decrypt
          </button>
        )}
        {isDecrypted && (
          <>
            <button
              onClick={() => onEdit(note.id, decryptedContent)}
              className="px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition text-sm"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(note.id)}
              className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition text-sm"
            >
              Delete
            </button>
          </>
        )}
      </div>
    </div>
  );
}
