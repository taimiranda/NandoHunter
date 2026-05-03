import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell } from "@/components/AppShell";
import { QUESTS } from "@/data/quests";

export const Route = createFileRoute("/history")({
  head: () => ({
    meta: [
      { title: "Journal — Nando the Hunter" },
      { name: "description", content: "Your hunting journal of accepted and rejected quests." },
    ],
  }),
  component: History,
});

const STATUS_STYLE: Record<string, string> = {
  accepted: "text-primary",
  rejected: "text-destructive",
  pending: "text-accent",
};

function History() {
  const entries = QUESTS.filter((q) => q.status !== "open");
  const counts = {
    accepted: entries.filter((e) => e.status === "accepted").length,
    rejected: entries.filter((e) => e.status === "rejected").length,
    pending: entries.filter((e) => e.status === "pending").length,
  };

  return (
    <AppShell title="HUNTER'S JOURNAL">
      <div className="pixel-panel p-4 grid grid-cols-3 text-center max-w-2xl mx-auto w-full">
        <Stat n={counts.accepted} label="ACCEPTED" color="text-primary" />
        <Stat n={counts.rejected} label="REJECTED" color="text-destructive" />
        <Stat n={counts.pending} label="PENDING" color="text-accent" />
      </div>

      <ol className="space-y-3">
        {entries.map((e) => (
          <li key={e.id}>
            <Link
              to="/quest/$id"
              params={{ id: e.id }}
              className="pixel-panel p-3 flex items-center gap-3 hover:border-accent transition h-full"
            >
              <div className="pixel text-[0.55rem] text-muted-foreground w-14 shrink-0">{e.date}</div>
              <div className="flex-1 min-w-0">
                <p className="text-base text-foreground truncate">{e.title}</p>
                <p className="text-sm text-muted-foreground truncate">⚒ {e.company}</p>
              </div>
              <span className={`pixel text-[0.5rem] ${STATUS_STYLE[e.status]} shrink-0`}>
                {e.status.toUpperCase()}
              </span>
            </Link>
          </li>
        ))}
      </ol>
    </AppShell>
  );
}

function Stat({ n, label, color }: { n: number; label: string; color: string }) {
  return (
    <div>
      <div className={`pixel text-lg ${color}`}>{n}</div>
      <div className="pixel text-[0.5rem] text-muted-foreground mt-1">{label}</div>
    </div>
  );
}
