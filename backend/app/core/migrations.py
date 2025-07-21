import asyncio
from typing import List, Callable
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import engine

class Migration:
    def __init__(self, version: int, description: str, up: Callable, down: Callable = None):
        self.version = version
        self.description = description
        self.up = up
        self.down = down

class MigrationManager:
    def __init__(self):
        self.migrations: List[Migration] = []
        self._migration_table_created = False

    def register(self, version: int, description: str):
        """Decorator to register migrations"""
        def decorator(func: Callable):
            self.migrations.append(Migration(version, description, func))
            return func
        return decorator

    async def create_migration_table(self, session: AsyncSession):
        """Create migration tracking table"""
        if self._migration_table_created:
            return

        # Create migration table if it doesn't exist
        await session.exec("""
            CREATE TABLE IF NOT EXISTS migrations (
                version INTEGER PRIMARY KEY,
                description TEXT,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await session.commit()
        self._migration_table_created = True

    async def get_applied_migrations(self, session: AsyncSession) -> List[int]:
        """Get list of applied migration versions"""
        await self.create_migration_table(session)
        result = await session.exec("SELECT version FROM migrations ORDER BY version")
        return [row[0] for row in result.all()]

    async def apply_migration(self, session: AsyncSession, migration: Migration):
        """Apply a single migration"""
        await migration.up(session)
        await session.exec(
            "INSERT INTO migrations (version, description) VALUES (?, ?)",
            (migration.version, migration.description)
        )
        await session.commit()

    async def run_migrations(self, session: AsyncSession):
        """Run all pending migrations"""
        applied = await self.get_applied_migrations(session)
        
        # Sort migrations by version
        pending_migrations = [
            m for m in sorted(self.migrations, key=lambda x: x.version)
            if m.version not in applied
        ]

        for migration in pending_migrations:
            print(f"Applying migration {migration.version}: {migration.description}")
            await self.apply_migration(session, migration)
            print(f"Migration {migration.version} applied successfully")

# Global migration manager
migration_manager = MigrationManager()

# Example migrations
@migration_manager.register(1, "Create initial tables")
async def create_initial_tables(session: AsyncSession):
    """Create all initial tables"""
    await session.run_sync(SQLModel.metadata.create_all)

@migration_manager.register(2, "Add indexes for performance")
async def add_performance_indexes(session: AsyncSession):
    """Add database indexes for better performance"""
    await session.exec("""
        CREATE INDEX IF NOT EXISTS idx_courses_start_date ON course(start_date);
        CREATE INDEX IF NOT EXISTS idx_courses_end_date ON course(end_date);
        CREATE INDEX IF NOT EXISTS idx_subjects_type ON subject(type);
        CREATE INDEX IF NOT EXISTS idx_difficulties_type ON difficulty(type);
    """)
    await session.commit()

async def run_migrations():
    """Run all database migrations"""
    async with engine.begin() as session:
        await migration_manager.run_migrations(session) 