// Mobile Resume Generator - Frontend

let currentJobInfo = null;

async function generate() {
    const jd = document.getElementById('jdInput').value.trim();
    if (!jd) {
        alert('Please paste a job description');
        return;
    }

    // Show loading
    document.getElementById('inputCard').style.display = 'none';
    document.getElementById('loading').classList.add('show');
    document.getElementById('result').classList.remove('show');
    document.getElementById('generateBtn').disabled = true;

    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_description: jd })
        });

        const data = await response.json();

        if (data.error) {
            throw new Error(data.error);
        }

        currentJobInfo = data.job_info;

        // Update UI with results
        document.getElementById('jobTitle').textContent = data.job_info.job_title || '-';
        document.getElementById('jobCompany').textContent = data.job_info.company || '-';
        document.getElementById('jobLocation').textContent = data.job_info.location || '-';
        document.getElementById('jobType').textContent = data.job_info.job_type || '-';

        // Skills
        const skillsContainer = document.getElementById('skills');
        skillsContainer.innerHTML = '';
        (data.job_info.key_skills || []).forEach(skill => {
            const span = document.createElement('span');
            span.className = 'skill';
            span.textContent = skill;
            skillsContainer.appendChild(span);
        });

        // Email
        document.getElementById('emailContent').textContent = data.email;

        // Show results
        document.getElementById('loading').classList.remove('show');
        document.getElementById('result').classList.add('show');

    } catch (error) {
        alert('Error: ' + error.message);
        document.getElementById('inputCard').style.display = 'block';
        document.getElementById('loading').classList.remove('show');
    }

    document.getElementById('generateBtn').disabled = false;
}

function copyEmail() {
    const email = document.getElementById('emailContent').textContent;
    navigator.clipboard.writeText(email).then(() => {
        showToast('Copied to clipboard!');
    });
}

function downloadResume(format) {
    if (!currentJobInfo) return;
    const company = (currentJobInfo.company || 'company').replace(/\s+/g, '_');
    window.open(`/api/resume/download?format=${format}&company=${company}`, '_blank');
}

function reset() {
    document.getElementById('inputCard').style.display = 'block';
    document.getElementById('result').classList.remove('show');
    document.getElementById('jdInput').value = '';
    currentJobInfo = null;
}

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
}

// PWA Service Worker Registration
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js').catch(() => {});
}

