
from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from src.llm import translate_text, process_user_notes
import json

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
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

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
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

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
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

@note_bp.route('/notes/process-natural-language', methods=['POST'])
def process_natural_language_note():
    """Process natural language input and create a structured note"""
    try:
        data = request.json
        if not data or 'user_input' not in data:
            return jsonify({'error': 'user_input is required'}), 400
        
        user_input = data['user_input']
        output_language = data.get('output_language', 'English')
        
        # Process the natural language input using LLM
        processed_result = process_user_notes(output_language, user_input)
        
        # Parse the JSON response from LLM
        try:
            note_data = json.loads(processed_result)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a fallback note
            note_data = {
                "Title": "AI Generated Note",
                "Notes": processed_result,
                "Tags": ["ai-generated"]
            }
        
        # Create the note in the database
        note = Note(
            title=note_data.get('Title', 'Untitled'),
            content=note_data.get('Notes', '')
        )
        
        db.session.add(note)
        db.session.commit()
        
        return jsonify({
            'note': note.to_dict(),
            'processed_data': note_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

