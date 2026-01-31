import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { notesAPI } from '../utils/api';
import NoteCard from './NoteCard';

export default function Notepad() {
  const [notes, setNotes] = useState([]);
  const [decryptedNotes, setDecryptedNotes] = useState({});
  const [newNoteContent, setNewNoteContent] = useState('');
  const [masterKey, setMasterKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [editingNoteId, setEditingNoteId] = useState(null);
  const [editingContent, setEditingContent] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    } else {
      loadNotes();
    }
  }, []);

  const loadNotes = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await notesAPI.getNotes();
      setNotes(response.data);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to load notes');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateNote = async (e) => {
    e.preventDefault();
    if (!newNoteContent.trim() || !masterKey.trim()) {
      setError('Note content and master key are required');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await notesAPI.createNote(newNoteContent, masterKey);
      setNewNoteContent('');
      setMessage('Note created successfully!');
      setTimeout(() => setMessage(''), 3000);
      loadNotes();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create note');
    } finally {
      setLoading(false);
    }
  };

  const handleDecryptNote = async (noteId) => {
    if (!masterKey.trim()) {
      setError('Master key is required to decrypt notes');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await notesAPI.decryptNote(noteId, masterKey);
      setDecryptedNotes({
        ...decryptedNotes,
        [noteId]: response.data.content,
      });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to decrypt note. Wrong master key?');
    } finally {
      setLoading(false);
    }
  };

  const handleEditNote = (noteId, content) => {
    setEditingNoteId(noteId);
    setEditingContent(content);
  };

  const handleSaveEdit = async (noteId) => {
    if (!editingContent.trim()) {
      setError('Note content cannot be empty');
      return;
    }

    if (!masterKey.trim()) {
      setError('Master key is required to update notes');
      return;
    }

    setLoading(true);
    setError('');
    try {
      await notesAPI.updateNote(noteId, editingContent, masterKey);
      setEditingNoteId(null);
      setMessage('Note updated successfully!');
      setTimeout(() => setMessage(''), 3000);
      loadNotes();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update note');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteNote = async (noteId) => {
    if (!window.confirm('Are you sure you want to delete this note? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    setError('');
    try {
      await notesAPI.deleteNote(noteId);
      setMessage('Note deleted successfully!');
      setTimeout(() => setMessage(''), 3000);
      loadNotes();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to delete note');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-800">Secure Notepad</h1>
          <div className="flex items-center gap-4">
            <span className="text-gray-600">Welcome, {localStorage.getItem('username')}</span>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Messages */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}
        {message && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {message}
          </div>
        )}

        {/* Master Key Input */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Master Key</h2>
          <p className="text-gray-600 text-sm mb-3">
            Enter your master key to encrypt/decrypt notes. This key is never stored and only used for the current session.
          </p>
          <input
            type="password"
            value={masterKey}
            onChange={(e) => setMasterKey(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your master key (required for all note operations)"
          />
        </div>

        {/* Create Note */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Create New Note</h2>
          <form onSubmit={handleCreateNote} className="space-y-4">
            <textarea
              value={newNoteContent}
              onChange={(e) => setNewNoteContent(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              rows="4"
              placeholder="Write your note here..."
            />
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Note'}
            </button>
          </form>
        </div>

        {/* Notes List */}
        <div>
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Your Notes ({notes.length})</h2>
          {loading && <p className="text-center text-gray-600">Loading...</p>}
          {notes.length === 0 && !loading && (
            <p className="text-center text-gray-600">No notes yet. Create your first note!</p>
          )}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {notes.map((note) =>
              editingNoteId === note.id ? (
                <div key={note.id} className="bg-white rounded-lg shadow-md p-6">
                  <textarea
                    value={editingContent}
                    onChange={(e) => setEditingContent(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none mb-3"
                    rows="4"
                  />
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleSaveEdit(note.id)}
                      disabled={loading}
                      className="flex-1 px-3 py-1 bg-green-500 text-white rounded hover:bg-green-600 transition disabled:opacity-50"
                    >
                      Save
                    </button>
                    <button
                      onClick={() => setEditingNoteId(null)}
                      className="flex-1 px-3 py-1 bg-gray-500 text-white rounded hover:bg-gray-600 transition"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              ) : (
                <NoteCard
                  key={note.id}
                  note={note}
                  onDecrypt={handleDecryptNote}
                  onEdit={handleEditNote}
                  onDelete={handleDeleteNote}
                  isDecrypted={decryptedNotes[note.id] !== undefined}
                  decryptedContent={decryptedNotes[note.id]}
                />
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
