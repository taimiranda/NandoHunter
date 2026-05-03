import { Link, useLocation } from "@tanstack/react-router";

const tabs = [
  { to: "/", icon: "🎯", label: "QUESTS" },
  { to: "/history", icon: "📜", label: "JOURNAL" },
  { to: "/settings", icon: "⚙", label: "GEAR" },
] as const;

export function TabBar() {
  const { pathname } = useLocation();
  const isActive = (to: string) => pathname === to || (to !== "/" && pathname.startsWith(to));

  return (
    <nav
      className="
        sticky bottom-0 z-20 pixel-panel mt-4 grid grid-cols-3 !rounded-none border-t-4
        md:hidden
      "
    >
      {tabs.map((t) => {
        const active = isActive(t.to);
        return (
          <Link
            key={t.to}
            to={t.to}
            className={`flex flex-col items-center gap-1 py-3 transition ${
              active ? "bg-input text-accent" : "text-muted-foreground"
            }`}
          >
            <span className="text-2xl leading-none">{t.icon}</span>
            <span className="pixel text-[0.55rem]">{t.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}

export function SideRail() {
  const { pathname } = useLocation();
  const isActive = (to: string) => pathname === to || (to !== "/" && pathname.startsWith(to));

  return (
    <aside className="hidden md:flex sticky top-4 self-start flex-col gap-2 pixel-panel p-3 w-44 lg:w-52">
      <div className="text-center pb-2 mb-1 border-b-2 border-border">
        <p className="pixel text-[0.5rem] text-accent tracking-widest">⚔ MENU ⚔</p>
      </div>
      {tabs.map((t) => {
        const active = isActive(t.to);
        return (
          <Link
            key={t.to}
            to={t.to}
            className={`flex items-center gap-3 px-3 py-3 border-2 transition ${
              active
                ? "bg-input border-accent text-accent"
                : "border-transparent text-muted-foreground hover:border-border hover:text-foreground"
            }`}
          >
            <span className="text-xl leading-none">{t.icon}</span>
            <span className="pixel text-[0.6rem]">{t.label}</span>
          </Link>
        );
      })}
    </aside>
  );
}
