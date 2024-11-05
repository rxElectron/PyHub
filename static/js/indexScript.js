console.log("Welcome to the Home Page!");

// Add click event listeners for each menu button
document.addEventListener('DOMContentLoaded', function() {
    // Dashboard button
    document.querySelector('.dashboard').addEventListener('click', function() {
        window.location.href = '/'; // Updated to match Flask route
    });

    // Learning button
    document.querySelector('.learning-exercises').addEventListener('click', function() {
        window.location.href = '/learning'; // Updated to match Flask route
    });

    // Consoles button
    document.querySelector('.coding-console').addEventListener('click', function() {
        window.location.href = '/live_console'; // Updated to match Flask route
    });

    // Workspace button
    document.querySelector('.project-manager').addEventListener('click', function() {
        window.location.href = '/project_manager'; // Updated to match Flask route
    });

    // Comparator button
    document.querySelector('.code-comparator').addEventListener('click', function() {
        window.location.href = '/code_comparator'; // Updated to match Flask route
    });

    // AI & ML Tools button
    document.querySelector('.ai-ml-tools').addEventListener('click', function() {
        window.location.href = '/ai_ml_tools'; // Updated to match Flask route
    });

    // Analytics button
    document.querySelector('.analytics').addEventListener('click', function() {
        window.location.href = '/analytics'; // Matches Flask route
    });

    // Settings button
    document.querySelector('.settings').addEventListener('click', function() {
        window.location.href = '/settings'; // Matches Flask route
    });

    // Support & Help button
    document.querySelector('.support-help').addEventListener('click', function() {
        window.location.href = '/support_help'; // Updated to match Flask route
    });
});
