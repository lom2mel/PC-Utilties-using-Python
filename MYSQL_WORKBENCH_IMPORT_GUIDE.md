# MySQL Workbench Import Guide

## Step-by-Step: Import SQL Dumps with Database Creation

### Step 1: Create the Database First

1. **Open MySQL Workbench**
2. **Connect to your MySQL server** (localhost)
3. **Create the database:**
   - Click the **SQL tab** (or press `Ctrl+Enter`)
   - Run this command:
   ```sql
   CREATE DATABASE IF NOT EXISTS provincial_gov_dbase 
   CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
   - Click the **lightning bolt** icon to execute

### Step 2: Import Using SQL Script

#### Method A: Run SQL Script (Recommended)

1. **Go to:** `File` → `Open SQL Script` (or press `Ctrl+Shift+O`)
2. **Navigate to:**
   ```
   C:\Users\Lomel\OneDrive - MSFT\Documents\dumps\dumps_110225\
   ```
3. **Select:** `provincial_gov_dbase_template_sync_history.sql`
4. **Set Default Schema:** 
   - Right-click `provincial_gov_dbase` in Navigator panel (left side)
   - Select **"Set as Default Schema"** (database name appears bold)
5. **Execute:** Click the lightning bolt icon or press `Ctrl+Shift+Enter`
6. **Wait** for "Action Output" to show completion

#### Method B: Import from Dump Project Folder (If Available)

1. **Go to:** `Server` → `Data Import`
2. **Select:** `Import from Dump Project Folder`
3. **Browse to folder:** 
   ```
   C:\Users\Lomel\OneDrive - MSFT\Documents\dumps\dumps_110225\
   ```
4. **Select Schema:** Check `provincial_gov_dbase`
5. **Click:** `Start Import`

### Step 3: Verify Import

```sql
USE provincial_gov_dbase;
SHOW TABLES;
SELECT COUNT(*) FROM template_sync_history;
```

## Quick Create All Databases

If you have multiple dumps to import, create all databases first:

```sql
-- Run this once to create all databases
CREATE DATABASE IF NOT EXISTS provincial_gov_dbase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS [other_database_name] CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Add more as needed based on your dump files
```

## Troubleshooting

### Error: "Unknown database"
**Solution:** Run the CREATE DATABASE command first (Step 1)

### Error: "Access denied"
**Solution:** Ensure you're connected as root or a user with CREATE/INSERT privileges

### Import is very slow
**Solution:** 
- Disable foreign key checks temporarily:
  ```sql
  SET foreign_key_checks = 0;
  -- Import here
  SET foreign_key_checks = 1;
  ```

### Large file import timeout
**Solution:**
- Increase timeouts in Workbench: `Edit` → `Preferences` → `SQL Editor`
- Set "DBMS connection read time out" to 600 seconds

## Batch Import Multiple Files

For your dumps directory with 9+ files:

1. **Create all databases first** (run the batch script)
2. **Import each file** using Data Import wizard
3. **Select correct target schema** for each file

Or use the Python script with `--auto-import` flag:
```bash
python src\mysql_import_helper.py "C:\Users\Lomel\OneDrive - MSFT\Documents\dumps\dumps_110225" --auto-import
```

---

**Pro Tip:** Always create the database BEFORE importing to avoid the "Unknown database" error!
