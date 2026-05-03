import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { AppShell } from "@/components/AppShell";
import { getQuest } from "@/data/quests";

export const Route = createFileRoute("/quest/$id")({
  loader: ({ params }) => {
    const quest = getQuest(params.id);
    if (!quest) throw notFound();
    return { quest };
  },
  head: ({ loaderData }) => ({
    meta: [
      { title: `${loaderData?.quest.title ?? "Quest"} — Nando the Hunter` },
      { name: "description", content: loaderData?.quest.reasoning ?? "Quest details" },
    ],
  }),
  component: QuestDetail,
  notFoundComponent: () => (
    <AppShell title="QUEST NOT FOUND">
      <div className="pixel-panel p-6 text-center space-y-3">
        <p className="pixel text-sm text-destructive">⚠ QUEST VANISHED</p>
        <Link to="/" className="pixel-btn pixel-btn-primary inline-block">↩ BACK TO BOARD</Link>
      </div>
    </AppShell>
  ),
});

const TIER = (s: number) =>
  s >= 8 ? { label: "LEGENDARY", color: "text-accent" } :
  s >= 6 ? { label: "RARE", color: "text-primary" } :
  { label: "COMMON", color: "text-muted-foreground" };

function QuestDetail() {
  const { quest } = Route.useLoaderData();
  const tier = TIER(quest.score);
  const isJournal = quest.status !== "open";

  const download = (kind: "resume" | "cover-letter") => {
    const text =
      kind === "resume"
        ? `# Fernando Almeida — Tailored Resume\n\nFor: ${quest.title} @ ${quest.company}\n\n## Summary\nReliable operations professional...\n`
        : `Dear ${quest.company} team,\n\nI'm excited to apply for ${quest.title}...\n\n— Fernando Almeida\n`;
    const blob = new Blob([text], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${kind}-${quest.id}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <AppShell title="QUEST DETAILS">
      <div className="max-w-3xl mx-auto w-full space-y-4">
        <Link to="/" className="pixel text-[0.6rem] text-muted-foreground hover:text-accent inline-block">
          ↩ BACK
        </Link>

        <article className="pixel-panel p-5 sm:p-6 space-y-4">
          <header className="space-y-2">
            <div className="flex items-center justify-between">
              <span className={`pixel text-[0.6rem] ${tier.color}`}>★ {tier.label}</span>
              <span className="pixel text-[0.7rem] text-[--gold]">{quest.score.toFixed(1)}/10</span>
            </div>
            <h2 className="pixel text-base sm:text-lg leading-tight">{quest.title}</h2>
            <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-base text-muted-foreground">
              <span>⚒ {quest.company}</span>
              <span>📍 {quest.location}</span>
              {quest.date && <span>🗓 {quest.date}</span>}
            </div>
          </header>

          <div className="h-1 bg-input border border-border">
            <div className="h-full bg-[--gold]" style={{ width: `${quest.score * 10}%` }} />
          </div>

          <p className="text-base italic text-foreground/90">"{quest.reasoning}"</p>

          <div className="flex flex-wrap gap-1">
            {quest.tags.map((t) => (
              <span key={t} className="pixel text-[0.5rem] px-2 py-1 bg-input border border-border">{t}</span>
            ))}
          </div>

          {quest.description && (
            <section className="space-y-2">
              <h3 className="pixel text-[0.65rem] text-accent">▸ QUEST BRIEFING</h3>
              <p className="text-base text-foreground/90 leading-relaxed">{quest.description}</p>
            </section>
          )}

          <section className="space-y-2">
            <h3 className="pixel text-[0.65rem] text-accent">▸ MATCH SCROLL</h3>
            <ul className="text-base text-foreground/80 border-l-2 border-accent pl-3 space-y-1">
              <li>✦ Strong ops & coordination match</li>
              <li>✦ Bilingual EN / PT bonus</li>
              <li>⚠ Years-of-experience window tight</li>
            </ul>
          </section>

          <div className="grid gap-2 sm:grid-cols-2 pt-2">
            {quest.url && (
              <a
                href={quest.url}
                target="_blank"
                rel="noreferrer"
                className="pixel-btn pixel-btn-accent text-center sm:col-span-2"
              >
                🔗 VIEW QUEST
              </a>
            )}

            {!isJournal ? (
              <>
                <button className="pixel-btn pixel-btn-primary">✓ ACCEPT</button>
                <button className="pixel-btn pixel-btn-danger">✗ REJECT</button>
              </>
            ) : (
              <>
                <button onClick={() => download("resume")} className="pixel-btn pixel-btn-primary">
                  📜 DOWNLOAD RESUME
                </button>
                <button onClick={() => download("cover-letter")} className="pixel-btn pixel-btn-primary">
                  ✉ DOWNLOAD COVER LETTER
                </button>
              </>
            )}
          </div>
        </article>
      </div>
    </AppShell>
  );
}
