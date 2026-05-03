export type QuestStatus = "open" | "accepted" | "rejected" | "pending";

export type Quest = {
  id: string;
  title: string;
  company: string;
  location: string;
  score: number;
  reasoning: string;
  tags: string[];
  status: QuestStatus;
  date?: string;
  url?: string;
  description?: string;
};

export const QUESTS: Quest[] = [
  {
    id: "1",
    title: "Property Operations Coordinator",
    company: "Mirabelli Corp",
    location: "Toronto, ON",
    score: 8.0,
    reasoning: "Strong fit — extensive operations experience and organizational skills align with the role.",
    tags: ["OPS", "ADMIN", "TENANT"],
    status: "open",
    url: "https://example.com/jobs/1",
    description:
      "Coordinate day-to-day property operations, support tenant communication, manage vendor scheduling, and keep workflows running smoothly across a portfolio of mixed-use buildings.",
  },
  {
    id: "2",
    title: "Office Services Coordinator",
    company: "The Globe and Mail",
    location: "Toronto, ON",
    score: 7.2,
    reasoning: "On-site coordination role matching workflow management and team support strengths.",
    tags: ["ON-SITE", "COORD", "TEAM"],
    status: "open",
    url: "https://example.com/jobs/2",
    description:
      "On-site office coordination supporting a busy editorial team. Manage facilities, vendor relationships, and cross-team logistics.",
  },
  {
    id: "3",
    title: "Inventory & Logistics Lead",
    company: "Northwind Supply",
    location: "Mississauga, ON",
    score: 6.4,
    reasoning: "Inventory coordination and stock organization match the master resume well.",
    tags: ["LOGISTICS", "INVENTORY"],
    status: "open",
    url: "https://example.com/jobs/3",
    description:
      "Lead inventory accuracy initiatives, coordinate inbound/outbound flows, and partner with warehouse teams.",
  },
  {
    id: "j1",
    title: "Operations Manager",
    company: "Greenleaf Co.",
    location: "Toronto, ON",
    score: 8.4,
    reasoning: "Excellent overlap with end-to-end operations leadership experience.",
    tags: ["OPS", "LEAD"],
    status: "accepted",
    date: "Day 142",
    url: "https://example.com/jobs/j1",
    description: "Own daily operations across a 40-person team. Build process, hire, and report to the COO.",
  },
  {
    id: "j2",
    title: "Admin Assistant",
    company: "Lakeshore Realty",
    location: "Toronto, ON",
    score: 4.2,
    reasoning: "Underutilizes operations leadership experience.",
    tags: ["ADMIN"],
    status: "rejected",
    date: "Day 140",
    description: "General admin support across leasing and property management teams.",
  },
  {
    id: "j3",
    title: "Logistics Planner",
    company: "Cedar & Pine",
    location: "Mississauga, ON",
    score: 7.6,
    reasoning: "Planning + inventory match resume strengths.",
    tags: ["LOGISTICS", "PLANNING"],
    status: "accepted",
    date: "Day 138",
    description: "Plan inbound logistics for a national retail brand.",
  },
  {
    id: "j4",
    title: "Office Lead",
    company: "Mirabelli Corp",
    location: "Toronto, ON",
    score: 7.0,
    reasoning: "On-site lead role aligned with coordination strengths.",
    tags: ["LEAD", "ON-SITE"],
    status: "pending",
    date: "Day 135",
    description: "Lead a small on-site office team supporting a busy property management firm.",
  },
  {
    id: "j5",
    title: "Workflow Analyst",
    company: "Northwind",
    location: "Remote",
    score: 5.1,
    reasoning: "Process focus is a fit but tooling stack is unfamiliar.",
    tags: ["ANALYST"],
    status: "rejected",
    date: "Day 130",
    description: "Analyze and improve cross-functional workflows for a logistics SaaS.",
  },
];

export const getQuest = (id: string) => QUESTS.find((q) => q.id === id);
