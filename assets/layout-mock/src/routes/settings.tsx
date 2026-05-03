import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/AppShell";
import hero from "@/assets/nando-hero.png";

export const Route = createFileRoute("/settings")({
  head: () => ({
    meta: [
      { title: "Gear & Profile — Nando the Hunter" },
      { name: "description", content: "Configure your hunter profile and master resume." },
    ],
  }),
  component: Settings,
});

function Settings() {
  return (
    <AppShell title="HUNTER'S GEAR">
      <div className="pixel-panel p-4 flex flex-col items-center text-center">
        <img src={hero} alt="Nando" className="w-40 h-auto -mb-2 drop-shadow-[0_4px_0_oklch(0_0_0/0.5)]" />
        <h2 className="pixel text-base text-accent mt-2">NANDO</h2>
        <p className="pixel text-[0.55rem] text-muted-foreground mt-1">RANGER · LV.7 · TORONTO</p>
      </div>

      <Field label="MASTER RESUME" rows={6} defaultValue={`# Fernando Almeida\nToronto, ON\n\n## Summary\nReliable operations professional with 10+ years of experience...`} />
      <Field label="TARGET PROFILE" rows={4} defaultValue={`Looking for: Operations / Coordination roles in Toronto.\nRemote OK. Bilingual EN / PT.`} />
      <Field label="HUNTING GROUNDS" rows={2} defaultValue={`linkedin, indeed, jobbank.gc.ca`} />

      <button className="pixel-btn pixel-btn-primary w-full">💾 SAVE LOADOUT</button>
    </AppShell>
  );
}

function Field({ label, rows, defaultValue }: { label: string; rows: number; defaultValue: string }) {
  return (
    <label className="block space-y-2">
      <span className="pixel text-[0.6rem] text-accent">▸ {label}</span>
      <textarea
        rows={rows}
        defaultValue={defaultValue}
        className="w-full bg-input border-2 border-border p-3 text-base font-mono text-foreground focus:outline-none focus:border-accent resize-none"
      />
    </label>
  );
}
