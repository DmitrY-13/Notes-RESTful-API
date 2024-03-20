class NoteCreationError(Exception):
    def __str__(self):
        return 'failed to create note'
