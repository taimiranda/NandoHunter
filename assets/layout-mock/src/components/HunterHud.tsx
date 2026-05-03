import avatar from "@/assets/nando-avatar.png";

export function HunterHud({ hp = 78, xp = 62, level = 7, gold = 1240 }) {
  return (
    <div className="pixel-panel p-3 flex items-center gap-3">
      <img
        src={avatar}
        alt="Nando the Hunter"
        className="w-16 h-16 rounded-sm border-2 border-border shrink-0"
      />
      <div className="flex-1 min-w-0">
        <div className="flex items-baseline justify-between gap-2">
          <span className="pixel text-[0.65rem] text-accent truncate">NANDO</span>
          <span className="pixel text-[0.6rem] text-muted-foreground">LV.{level}</span>
        </div>
        <Bar label="HP" value={hp} color="bg-[--hp]" />
        <Bar label="XP" value={xp} color="bg-[--mp]" />
        <div className="flex items-center justify-between mt-1">
          <span className="pixel text-[0.55rem] text-muted-foreground">QUESTS</span>
          <span className="pixel text-[0.65rem] text-[--gold]">◆ {gold}</span>
        </div>
      </div>
    </div>
  );
}

function Bar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex items-center gap-2 mt-1">
      <span className="pixel text-[0.5rem] w-6 text-muted-foreground">{label}</span>
      <div className="flex-1 h-2 bg-input border border-border">
        <div className={`h-full ${color}`} style={{ width: `${value}%` }} />
      </div>
    </div>
  );
}
