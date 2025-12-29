import type { AstroIntegration } from 'astro';
import { parse } from '@astrojs/compiler';
import { readFileSync } from 'fs';

function getRelativePath(filePath: string): string {
  return filePath.replace(/^.*\/src\//, 'src/');
}

export function vueNodeTransform() {
  return (node: any, ctx: any) => {
    if (node && node.type === 1 && node.tag) {
      const filePath = ctx?.filename || '';
      const relativeFile = getRelativePath(filePath);

      const hasSourceAttr = node.props.some(
        (prop: any) => prop.type === 6 && prop.name === 'data-source-file'
      );
      if (!hasSourceAttr) {
        node.props.push(
          { type: 6, name: 'data-source-file', value: { content: relativeFile } },
          { type: 6, name: 'data-source-line-start', value: { content: String(node.loc.start.line) } },
          { type: 6, name: 'data-source-line-end', value: { content: String(node.loc.end.line) } }
        );
      }
    }
  };
}

function injectLocationVitePlugin() {
  return {
    name: 'vite-plugin-astro-inject-location',
    enforce: 'pre' as const,

    async load(id: string) {
      if (!id.endsWith('.astro')) {
        return null;
      }

      try {
        const sourceCode = readFileSync(id, 'utf-8');
        const relativePath = getRelativePath(id);
        const ast = await parse(sourceCode, { position: true });
        const elementsToInject: Array<{ line: number; endLine: number; name: string }> = [];

        function collectElements(node: any, inExpression = false) {
          if (!node) return;

          const isExpression = node.type === 'expression';
          const currentInExpression = inExpression || isExpression;

          if (!currentInExpression && node.type === 'element' && node.position && node.name) {
            if (!['script', 'style', 'Fragment', 'slot'].includes(node.name) && 
                node.position.start && node.position.end) {
              elementsToInject.push({
                line: node.position.start.line,
                endLine: node.position.end.line,
                name: node.name
              });
            }
          }

          for (const key in node) {
            if (key === 'parent') continue;
            const value = node[key];
            if (Array.isArray(value)) {
              value.forEach(child => collectElements(child, currentInExpression));
            } else if (typeof value === 'object' && value !== null && value.type) {
              collectElements(value, currentInExpression);
            }
          }
        }

        if (ast) {
          collectElements(ast);
        }

        if (elementsToInject.length === 0) {
          return null;
        }

        const lines = sourceCode.split('\n');
        const processedLines = new Set<number>();

        elementsToInject.forEach(element => {
          const lineIndex = element.line - 1;

          if (lineIndex >= 0 && lineIndex < lines.length && !processedLines.has(lineIndex)) {
            const line = lines[lineIndex];
            const tagRegex = new RegExp(`<(${element.name})([\\s>/])`);
            const match = tagRegex.exec(line);

            if (match) {
              const attrs = [
                `data-source-file="${relativePath}"`,
                `data-source-line-start="${element.line}"`,
                `data-source-line-end="${element.endLine}"`
              ].join(' ');

              const before = line.substring(0, match.index + 1 + element.name.length);
              const after = line.substring(match.index + 1 + element.name.length);
              lines[lineIndex] = `${before} ${attrs}${after}`;
              processedLines.add(lineIndex);
            }
          }
        });

        return {
          code: lines.join('\n'),
          map: null,
        };
      } catch (e) {
        console.error(`Failed to process ${id}:`, e);
        return null;
      }
    },
  };
}

export function astroSourceIntegration(): AstroIntegration {
  return {
    name: 'astro-source-integration',
    hooks: {
      'astro:config:setup': ({ updateConfig }) => {
        updateConfig({
          vite: {
            plugins: [injectLocationVitePlugin()],
          },
        });
      }
    }
  };
}
