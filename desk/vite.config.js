import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import frappeui from "frappe-ui/vite";
import path from "path";
import IconsResolver from "unplugin-icons/resolver";
import Components from "unplugin-vue-components/vite";
import { defineConfig } from "vite";
import { VitePWA } from "vite-plugin-pwa";
import fs from "fs";

function appPath(app) {
  const root = path.resolve(__dirname, "../.."); // points to apps
  const frontendPaths = [
    // Standard frontend structure: appname/frontend/src
    path.join(root, app, "frontend", "src"),
    // Desk-based apps: appname/desk/src
    path.join(root, app, "desk", "src"),
    // Alternative frontend structures
    path.join(root, app, "client", "src"),
    path.join(root, app, "ui", "src"),
    // Direct src structure: appname/src
    path.join(root, app, "src"),
  ];
  return frontendPaths.find((srcPath) => fs.existsSync(srcPath)) || null;
}

function hasApp(app) {
  return fs.existsSync(appPath(app));
}

// List of frontend apps used in this project
let apps = ["telephony"];

const alias = [
  // Default "@" for this app
  {
    find: "@",
    replacement: path.resolve(__dirname, "src"),
  },
  {
    find: "tailwind.config.js",
    replacement: path.resolve(__dirname, "tailwind.config.js"),
  },

  // App-specific aliases like @helpdesk, @hrms, etc.
  ...apps.map((app) =>
    hasApp(app)
      ? { find: `@${app}`, replacement: appPath(app) }
      : { find: `@${app}`, replacement: `virtual:${app}` }
  ),
];

export default defineConfig({
  plugins: [
    frappeui({
      frappeProxy: true,
      lucideIcons: true,
      jinjaBootData: true,
      buildConfig: {
        outDir: `../helpdesk/public/desk`,
        emptyOutDir: true,
        indexHtmlPath: "../helpdesk/www/helpdesk/index.html",
      },
    }),
    vue(),
    vueJsx(),
    Components({
      resolvers: IconsResolver({
        prefix: false,
        enabledCollections: ["lucide"],
      }),
    }),
    VitePWA({
      registerType: "autoUpdate",
      devOptions: {
        enabled: true,
      },
      workbox: {
        cleanupOutdatedCaches: true,
        maximumFileSizeToCacheInBytes: 5 * 1024 * 1024,
      },
      manifest: {
        display: "standalone",
        name: "Frappe Helpdesk",
        short_name: "Helpdesk",
        start_url: "/helpdesk",
        description:
          "Modern, Streamlined, Free and Open Source Customer Service Software",
        icons: [
          {
            src: "/assets/helpdesk/desk/manifest/manifest-icon-192.maskable.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "any",
          },
          {
            src: "/assets/helpdesk/desk/manifest/manifest-icon-192.maskable.png",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable",
          },
          {
            src: "/assets/helpdesk/desk/manifest/manifest-icon-512.maskable.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "any",
          },
          {
            src: "/assets/helpdesk/desk/manifest/manifest-icon-512.maskable.png",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable",
          },
        ],
      },
    }),
  ],
  resolve: {
    alias,
  },
  optimizeDeps: {
    include: [
      "feather-icons",
      "showdown",
      "tailwind.config.js",
      "prosemirror-state",
      "prosemirror-view",
      "lowlight",
    ],
  },
});
