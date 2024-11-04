console.log("Welcome to the Home Page!");
// Add click event listeners for each menu button
document.addEventListener('DOMContentLoaded', function() {
    // Dashboard button
    document.querySelector('.dashboard').addEventListener('click', function() {
        window.location.href = '/dashboard';
    });

    // Terminals button
    document.querySelector('.coding-console').addEventListener('click', function() {
        window.location.href = '/terminals';
    });

    // Debugger button
    document.querySelector('.debugger').addEventListener('click', function() {
        window.location.href = '/debugger';
    });

    // Learning Exercises button
    document.querySelector('.learning-exercises').addEventListener('click', function() {
        window.location.href = '/exercises';
    });

    // Project Manager button
    document.querySelector('.project-manager').addEventListener('click', function() {
        window.location.href = '/workspace';
    });

    // Code Comparator button
    document.querySelector('.code-comparator').addEventListener('click', function() {
        window.location.href = '/comparator';
    });

    // AI & ML Tools button
    document.querySelector('.ai-ml-tools').addEventListener('click', function() {
        window.location.href = '/ai-tools';
    });

    // Analytics button
    document.querySelector('.analytics').addEventListener('click', function() {
        window.location.href = '/analytics';
    });

    // Settings button
    document.querySelector('.settings').addEventListener('click', function() {
        window.location.href = '/settings';
    });

    // Support & Help button
    document.querySelector('.support-help').addEventListener('click', function() {
        window.location.href = '/support';
    });
});
