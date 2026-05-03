import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/AppShell";
import { HunterHud } from "@/components/HunterHud";
import { QuestCard } from "@/components/QuestCard";
import { QUESTS } from "@/data/quests";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Nando the Hunter — Quest Board" },
      { name: "description", content: "Indie-game styled job hunting app. Track legendary roles." },
    ],
  }),
  component: Quests,
});

function Quests() {
  const open = QUESTS.filter((q) => q.status === "open");
  return (
    <AppShell title="QUEST BOARD">
      <div className="space-y-6">
        <section className="pixel-panel p-4 flex flex-col sm:flex-row sm:items-center gap-4">
          <div className="flex-1"><HunterHud /></div>
          <div className="flex flex-col gap-2 sm:w-56">
            <button className="pixel-btn pixel-btn-primary w-full">▶ HUNT</button>
            <label className="flex items-center gap-2 text-base text-muted-foreground">
              <input type="checkbox" className="accent-accent w-4 h-4" />
              Show low-tier (below 5)
            </label>
          </div>
        </section>

        <section className="space-y-4">
          {open.map((q) => <QuestCard key={q.id} quest={q} />)}
        </section>
      </div>
    </AppShell>
  );
}
