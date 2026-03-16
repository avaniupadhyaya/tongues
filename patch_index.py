content = open('templates/index.html').read()

# 1. Add CSS before closing </style>
css = """
    .feedback-banner {
      margin-top: 32px;
      background: linear-gradient(135deg, #FFF8F2, #FFF3E8);
      border: 1.5px solid #F5C89A;
      border-radius: 20px;
      padding: 20px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .feedback-banner-text { flex: 1; min-width: 200px; }
    .feedback-banner-text strong {
      font-size: 15px; font-weight: 600; color: var(--ink);
      display: block; margin-bottom: 4px;
    }
    .feedback-banner-text span { font-size: 13px; color: var(--ink-light); }
    .feedback-banner-btn {
      padding: 10px 24px;
      background: linear-gradient(135deg, #E8651A, #D4561A);
      color: white; border: none; border-radius: 100px;
      font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600;
      cursor: pointer; white-space: nowrap;
      box-shadow: 0 4px 12px rgba(232,101,26,0.3);
      transition: all 0.2s; text-decoration: none; display: inline-block;
    }
    .feedback-banner-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(232,101,26,0.4);
    }
    @media (max-width: 600px) {
      .feedback-banner { flex-direction: column; text-align: center; }
    }
"""

content = content.replace('  </style>', css + '  </style>', 1)

# 2. Add banner HTML between card and footer
banner = """
  <div class="feedback-banner">
    <div class="feedback-banner-text">
      <strong>🙏 Help make Tongues better</strong>
      <span>Tried the app? Share your experience — it takes just 2 minutes.</span>
    </div>
    <a class="feedback-banner-btn" href="https://forms.gle/N3qxcdPxM8GuqzC37" target="_blank" rel="noopener">Share Feedback ↗</a>
  </div>

"""

content = content.replace('  <footer>', banner + '  <footer>', 1)
open('templates/index.html', 'w').write(content)
print('Done — feedback banner added to index.html')
