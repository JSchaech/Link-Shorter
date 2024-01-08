function deleteEntry(entryId) {
    // Confirm deletion (optional)
    if (confirm("Are you sure you want to delete this entry?")) {
        // Send an AJAX request to the server to delete the entry
        fetch(`/delete_entry/${entryId}`, {
            method: 'DELETE',
        })
        .catch(error => console.error('Error:', error));
        setTimeout(function () {
            location.reload();
        }, 500);
    }
}