
"use client";

import { useState } from "react";
import {
  LayoutDashboard,
  Users,
  UserSearch,
  Bot,
  FileText,
  Settings,
  Bell,
  Search,
  TrendingUp,
  Clock,
  CheckCircle,
  Menu,
} from "lucide-react";

const navigation = [
  { label: "Dashboard", icon: LayoutDashboard },
  { label: "Clients", icon: Users },
  { label: "Leads", icon: UserSearch },
  { label: "AI Agents", icon: Bot },
  { label: "Deliverables", icon: FileText },
  { label: "Settings", icon: Settings },
];

const stats = [
  { label: "Total Clients", value: "0", icon: Users, note: "No clients added yet" },
  { label: "Active Leads", value: "0", icon: UserSearch, note: "Start generating leads" },
  { label: "Active Tasks", value: "0", icon: Clock, note: "No running tasks" },
  { label: "Completed Tasks", value: "0", icon: CheckCircle, note: "No completed tasks" },
];

export default function DashboardPage() {
  const [activePage, setActivePage] = useState("Dashboard");
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <main className="dashboard">
      <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon">A</div>
          <div>
            <strong>SEO AGENCY</strong>
            <span>AI Management Platform</span>
          </div>
        </div>

        <p className="nav-heading">WORKSPACE</p>

        <nav>
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.label}
                className={`nav-item ${activePage === item.label ? "active" : ""}`}
                onClick={() => {
                  setActivePage(item.label);
                  setMenuOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="admin-avatar">SA</div>
          <div>
            <strong>Agency Admin</strong>
            <span>Super Admin</span>
          </div>
        </div>
      </aside>

      <section className="main-area">
        <header className="topbar">
          <button className="mobile-menu" onClick={() => setMenuOpen(!menuOpen)}>
            <Menu size={22} />
          </button>

          <div className="breadcrumb">
            Workspace <span>/</span> {activePage}
          </div>

          <div className="top-actions">
            <button className="icon-button" aria-label="Search">
              <Search size={19} />
            </button>
            <button className="icon-button" aria-label="Notifications">
              <Bell size={19} />
            </button>
            <div className="top-avatar">SA</div>
          </div>
        </header>

        <div className="page-content">
          <div className="welcome-row">
            <div>
              <p className="eyebrow">AGENCY OVERVIEW</p>
              <h1>{activePage}</h1>
              <p className="subtitle">
                Welcome to your private AI SEO agency workspace.
              </p>
            </div>
            <div className="date-label">ADMIN WORKSPACE</div>
          </div>

          <div className="stats-grid">
            {stats.map((stat) => {
              const Icon = stat.icon;
              return (
                <article className="stat-card" key={stat.label}>
                  <div className="stat-top">
                    <span>{stat.label}</span>
                    <div className="stat-icon"><Icon size={20} /></div>
                  </div>
                  <h2>{stat.value}</h2>
                  <p>{stat.note}</p>
                </article>
              );
            })}
          </div>

          <div className="content-grid">
            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h3>Agency Performance</h3>
                  <p>Your workspace activity overview</p>
                </div>
                <TrendingUp size={21} />
              </div>

              <div className="empty-state">
                <div className="empty-icon"><TrendingUp size={26} /></div>
                <strong>Analytics will appear here</strong>
                <p>Add clients and projects to start tracking agency performance.</p>
              </div>
            </section>

            <section className="panel">
              <div className="panel-heading">
                <div>
                  <h3>Recent Activity</h3>
                  <p>Latest agency updates</p>
                </div>
                <Clock size={20} />
              </div>

              <div className="empty-state">
                <div className="empty-icon"><Bell size={25} /></div>
                <strong>No recent activity</strong>
                <p>New client and agent activities will appear here.</p>
              </div>
            </section>
          </div>

          <footer className="footer">
            AI SEO Agency Platform · Private Admin Workspace
          </footer>
        </div>
      </section>
    </main>
  );
}
