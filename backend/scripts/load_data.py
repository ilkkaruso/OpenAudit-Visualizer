import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal, engine
from app import models

def load_unliquidated_data(csv_path: str):
    db = SessionLocal()

    try:
        print("Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        print("Tables created successfully")

        print(f"Reading CSV file from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} records from CSV")

        lgu_cache = {}
        transaction_count = 0

        print("Processing records...")
        for idx, row in df.iterrows():
            # Skip rows with missing critical data
            if pd.isna(row['lgu']) or pd.isna(row['year']) or pd.isna(row['unliquidated']):
                continue

            lgu_name = str(row['lgu'])
            province = str(row['province']) if not pd.isna(row['province']) else None
            year = int(row['year'])
            amount = float(row['unliquidated'])

            lgu_key = (lgu_name, province)

            if lgu_key not in lgu_cache:
                existing_lgu = db.query(models.LocalGovernment).filter(
                    models.LocalGovernment.name == lgu_name,
                    models.LocalGovernment.province == province
                ).first()

                if not existing_lgu:
                    lgu = models.LocalGovernment(
                        name=lgu_name,
                        province=province
                    )
                    db.add(lgu)
                    db.flush()
                    lgu_cache[lgu_key] = lgu.id
                else:
                    lgu_cache[lgu_key] = existing_lgu.id

            lgu_id = lgu_cache[lgu_key]

            transaction = models.UnliquidatedTransaction(
                lgu_id=lgu_id,
                year=year,
                amount=amount
            )
            db.add(transaction)
            transaction_count += 1

            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1}/{len(df)} records...")
                db.commit()

        db.commit()
        print(f"\nData loading complete!")
        print(f"Total LGUs: {len(lgu_cache)}")
        print(f"Total transactions: {transaction_count}")

    except Exception as e:
        print(f"Error loading data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    csv_file = Path(__file__).parent.parent.parent / "unliquidata1024.csv"

    if not csv_file.exists():
        print(f"Error: CSV file not found at {csv_file}")
        sys.exit(1)

    load_unliquidated_data(str(csv_file))
