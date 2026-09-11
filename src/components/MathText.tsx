import React from 'react';
import katex from 'katex';

interface MathTextProps {
  content: string;
  className?: string;
  block?: boolean;
}

/**
 * Renders text containing inline ($...$) and block ($$...$$) KaTeX math expressions.
 * Regular text and code blocks are rendered cleanly.
 */
export const MathText: React.FC<MathTextProps> = ({ content, className = '', block = false }) => {
  if (!content) return null;

  // Function to safely render KaTeX
  const renderMath = (latex: string, isBlock: boolean): string => {
    try {
      return katex.renderToString(latex, {
        displayMode: isBlock,
        throwOnError: false,
      });
    } catch {
      return latex;
    }
  };

  // Parse block math $$...$$ first, then inline $...$
  const parseContent = (text: string): React.ReactNode[] => {
    // Regex matches $$...$$ or $...$
    const parts = text.split(/(\$\$[\s\S]*?\$\$|\$[^\$\n]+?\$)/g);

    return parts.map((part, index) => {
      if (part.startsWith('$$') && part.endsWith('$$')) {
        const math = part.slice(2, -2).trim();
        const html = renderMath(math, true);
        return (
          <div
            key={index}
            className="my-2 overflow-x-auto py-1 text-center"
            dangerouslySetInnerHTML={{ __html: html }}
          />
        );
      } else if (part.startsWith('$') && part.endsWith('$')) {
        const math = part.slice(1, -1).trim();
        const html = renderMath(math, false);
        return (
          <span
            key={index}
            className="inline-block px-0.5"
            dangerouslySetInnerHTML={{ __html: html }}
          />
        );
      }
      // Return normal text or line breaks
      return <React.Fragment key={index}>{part}</React.Fragment>;
    });
  };

  if (block) {
    return <div className={`math-content ${className}`}>{parseContent(content)}</div>;
  }

  return <span className={`math-content ${className}`}>{parseContent(content)}</span>;
};

export default MathText;
