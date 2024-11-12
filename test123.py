async function pushNewFile(fileName, content, providedLanguage = null) {
    try {
        const { githubToken, githubRepo, githubUsername } = await chrome.storage.sync.get([
            'githubToken',
            'githubRepo',
            'githubUsername'
        ]);

        if (!githubToken || !githubRepo || !githubUsername) {
            throw new Error("Missing GitHub settings");
        }

        // Detect language and add extension if needed
        const detectedLanguage = detectLanguage(fileName, content);
        console.log('Detected language:', detectedLanguage);

        // Add appropriate extension if none exists
        let finalFileName = fileName;
        if (!fileName.includes('.') && detectedLanguage) {
            const extensions = {
                python: '.py',
                javascript: '.js',
                java: '.java'
            };
            finalFileName = `${fileName}${extensions[detectedLanguage] || ''}`;
        }

        // First, check if file exists and get its SHA if it does
        const checkFileResponse = await fetch(
            `https://api.github.com/repos/${githubUsername}/${githubRepo}/contents/${finalFileName}`,
            {
                headers: {
                    'Authorization': `token ${githubToken}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            }
        );

        let existingSha = null;
        if (checkFileResponse.status === 200) {
            const fileData = await checkFileResponse.json();
            existingSha = fileData.sha;
            console.log('Existing file found, SHA:', existingSha);
        }

        // Get default branch
        const branchResponse = await fetch(
            `https://api.github.com/repos/${githubUsername}/${githubRepo}`,
            {
                headers: {
                    'Authorization': `token ${githubToken}`,
                    'Accept': 'application/vnd.github.v3+json'
                }
            }
        );

        if (!branchResponse.ok) {
            throw new Error('Failed to get repository information');
        }

        const repoInfo = await branchResponse.json();
        const defaultBranch = repoInfo.default_branch;

        // Prepare content and message
        const base64Content = btoa(unescape(encodeURIComponent(content)));
        const commitMessage = detectedLanguage 
            ? `${existingSha ? 'Update' : 'Add'} ${detectedLanguage} file: ${finalFileName}` 
            : `${existingSha ? 'Update' : 'Add'} file: ${finalFileName}`;

        // Prepare request body
        const requestBody = {
            message: commitMessage,
            content: base64Content,
            branch: defaultBranch
        };

        // Include SHA if file exists
        if (existingSha) {
            requestBody.sha = existingSha;
        }

        // Push the file
        const response = await fetch(
            `https://api.github.com/repos/${githubUsername}/${githubRepo}/contents/${finalFileName}`,
            {
                method: 'PUT',
                headers: {
                    'Authorization': `token ${githubToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestBody)
            }
        );

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to push file');
        }

        const responseData = await response.json();
        return {
            success: true,
            language: detectedLanguage || 'unknown',
            fileName: finalFileName,
            path: responseData.content.path,
            message: `File ${existingSha ? 'updated' : 'created'} successfully in ${defaultBranch}`,
            url: responseData.content.html_url
        };
    } catch (error) {
        console.error("Error pushing file:", error);
        return {
            success: false,
            message: error.message
        };
    }
}

// Keep your existing detectLanguage function and message listener
