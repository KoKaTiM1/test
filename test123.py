function addPushButton(codeBlock) {
    // Check if button already exists to avoid duplicates
    if (!codeBlock.nextElementSibling || !codeBlock.nextElementSibling.classList.contains('push-button')) {
        const pushButton = document.createElement('button');
        pushButton.textContent = 'Push to GitHub';
        pushButton.classList.add('push-button');
        
        // Style the button to match GitHub's green color
        pushButton.style.backgroundColor = '#2ea44f'; // GitHub green
        pushButton.style.color = '#ffffff';           // White text
        pushButton.style.border = 'none';
        pushButton.style.borderRadius = '6px';
        pushButton.style.padding = '8px 16px';
        pushButton.style.fontSize = '14px';
        pushButton.style.cursor = 'pointer';
        pushButton.style.marginTop = '10px';
        pushButton.style.display = 'block';

        // Add hover effect for better UX
        pushButton.addEventListener('mouseover', () => {
            pushButton.style.backgroundColor = '#2c974b'; // Darker green on hover
        });
        pushButton.addEventListener('mouseout', () => {
            pushButton.style.backgroundColor = '#2ea44f'; // Revert to original color
        });

        pushButton.addEventListener('click', () => {
            const content = codeBlock.textContent;
            const fileName = prompt("Enter file name:");
            if (fileName) {
                pushToGitHub(fileName, content);
            }
        });

        // Append the button below the code block
        codeBlock.parentNode.insertBefore(pushButton, codeBlock.nextSibling);
        console.log("Push button added below code block.");
    }
}
