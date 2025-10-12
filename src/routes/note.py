
from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from src.llm import translate_text

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes/<uuid:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate a note's title and content to a target language using LLM"""
    note = Note.query.get_or_404(note_id)
    data = request.json or {}
    target_language = data.get('target_language', 'Chinese')
    try:
        translated_title = translate_text(note.title, target_language=target_language)
        translated_content = translate_text(note.content, target_language=target_language)
        return jsonify({
            'translated_title': translated_title,
            'translated_content': translated_content
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by most recently updated"""
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        
        note = Note(title=data['title'], content=data['content'])
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<uuid:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a note"""

@note_bp.route('/notes/<uuid:note_id>', methods=['PUT'])
def edit_note(note_id):
    """Edit a note's title and content"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<uuid:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

