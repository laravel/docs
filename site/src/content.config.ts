import { defineCollection } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { z } from 'astro/zod';

export const collections = {
  docs: defineCollection({
    // Preserve dots in version segments (13.x) instead of slugifying them to 13x.
    loader: docsLoader({ generateId: ({ entry }) => entry.replace(/\.mdx?$/, '').replace(/(^|\/)index$/, '') }),
    schema: docsSchema({
      extend: z.object({ translationSourceCommit: z.string().regex(/^[a-f0-9]{40}$/).optional() }),
    }),
  }),
};
