import { Link } from "@tanstack/react-router";
import { useState } from "react";
import type { Quest } from "@/data/quests";

export function QuestCard({ quest }: { quest: Quest }) {
  const [open, setOpen] = useState(false);
  const tier =
    quest.score >= 8 ? { label: "LEGENDARY", color: "text-accent" } :
    quest.score >= 6 ? { label: "RARE", color: "text-primary" } :
    { label: "COMMON", color: "text-muted-foreground" };

  return (
    <article className="pixel-panel p-4 space-y-3 h-full flex flex-col">
      <header className="space-y-1">
        <div className="flex items-center justify-between gap-2">
          <span className={`pixel text-[0.55rem] ${tier.color}`}>★ {tier.label}</span>
          <span className="pixel text-[0.6rem] text-[--gold]">{quest.score.toFixed(1)}/10</span>
        </div>
        <h2 className="pixel text-sm leading-tight text-foreground">{quest.title}</h2>
        <div className="flex items-center justify-between text-base text-muted-foreground">
          <span className="truncate">⚒ {quest.company}</span>
          <span className="text-xs">📍 {quest.location}</span>
        </div>
      </header>

      <div className="h-1 bg-input border border-border">
        <div className="h-full bg-[--gold]" style={{ width: `${quest.score * 10}%` }} />
      </div>

      <p className="text-base text-foreground/90 italic leading-snug">"{quest.reasoning}"</p>

      <div className="flex flex-wrap gap-1">
        {quest.tags.map((t) => (
          <span key={t} className="pixel text-[0.5rem] px-2 py-1 bg-input border border-border">{t}</span>
        ))}
      </div>

      <button
        onClick={() => setOpen(!open)}
        className="w-full text-left pixel text-[0.6rem] text-muted-foreground border-2 border-dashed border-border px-3 py-2 hover:text-accent"
      >
        {open ? "▼" : "▶"} MATCH SCROLL
      </button>
      {open && (
        <div className="text-base text-foreground/80 border-l-2 border-accent pl-3 space-y-1">
          <p>✦ Strong ops & coordination match</p>
          <p>✦ Bilingual EN / PT bonus</p>
          <p>⚠ Years-of-experience window tight</p>
        </div>
      )}

      <div className="mt-auto pt-1">
        <Link
          to="/quest/$id"
          params={{ id: quest.id }}
          className="pixel-btn pixel-btn-accent w-full text-center block"
        >
          ⚔ VIEW QUEST
        </Link>
      </div>
    </article>
  );
}
