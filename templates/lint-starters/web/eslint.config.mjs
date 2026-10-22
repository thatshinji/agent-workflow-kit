// ESLint flat config starter (web stack: TypeScript + React).
// Copy to your web app root as eslint.config.mjs.
// "New code only" is not a config option here — CI lints just the files
// a PR touches. See ../README.md for the command.
// @ts-check

import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";

export default tseslint.config(
  {
    // Build output is never linted.
    ignores: ["dist/**"],
  },

  // TypeScript recommended rules.
  ...tseslint.configs.recommended,

  {
    plugins: {
      "react-hooks": reactHooks,
    },
    rules: {
      // Hooks rules: calling hooks conditionally or in the wrong order
      // corrupts state silently, so these stay on.
      ...reactHooks.configs.recommended.rules,

      // `any` switches the type system off exactly where someone was in
      // a hurry. As a "warn" this has no constraining power over an AI
      // writer — the build stays green either way — so it is an error.
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
);
