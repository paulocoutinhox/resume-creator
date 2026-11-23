import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

// builds the css and js bundle that the python-rendered html files reference.
// paths are relative to this config file (frontend/).
export default defineConfig({
    plugins: [tailwindcss()],
    build: {
        outDir: "../build/web/assets",
        emptyOutDir: true,
        manifest: false,
        rollupOptions: {
            input: "src/main.js",
            output: {
                entryFileNames: "main.js",
                chunkFileNames: "[name].js",
                assetFileNames: "[name][extname]",
            },
        },
    },
});
