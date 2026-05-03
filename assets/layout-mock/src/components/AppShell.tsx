import { ReactNode } from "react";
import { TabBar, SideRail } from "./TabBar";

export function AppShell({ children, title }: { children: ReactNode; title: string }) {
  return (
    <div className="mx-auto max-w-7xl min-h-screen flex flex-col px-4 sm:px-6 lg:px-8 pt-5 pb-2">
      <header className="text-center mb-6">
        <p className="pixel text-[0.55rem] sm:text-[0.65rem] text-accent tracking-widest">⚔ EST. MMXXVI ⚔</p>
        <h1 className="pixel text-xl sm:text-3xl lg:text-4xl text-foreground mt-2">
          NANDO <span className="text-primary">THE HUNTER</span>
        </h1>
        <p className="pixel text-[0.55rem] sm:text-[0.65rem] text-muted-foreground mt-2">— {title} —</p>
      </header>

      <div className="flex-1 flex gap-6">
        <SideRail />
        <main className="flex-1 min-w-0 space-y-4">{children}</main>
      </div>

      <TabBar />
    </div>
  );
}
