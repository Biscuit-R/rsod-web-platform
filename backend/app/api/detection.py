import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.detection_service import detection_service
from app.utils.file_utils import save_upload_file, ensure_directories
from app.utils.auth_utils import get_current_user
from app.database import get_db
from app.models.db_models import User, DetectionHistory
from app.config import settings
from app.models.schemas import SingleDetectionResponse, TargetListResponse, TargetItem

router = APIRouter(prefix="/detection", tags=["detection"])

ensure_directories()


@router.post("/single", response_model=SingleDetectionResponse)
async def detect_single_image(
    file: UploadFile = File(...),
    model_name: str = Form("pest-v1"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        filename = await save_upload_file(file, settings.UPLOAD_DIR)
        image_path = os.path.join(settings.UPLOAD_DIR, filename)

        result = detection_service.detect_single_image(image_path, model_name)

        # 保存检测记录到数据库
        history = DetectionHistory(
            user_id=current_user.id,
            filename=filename,
            original_image=result.image_url,
            result_image=result.result_image_url,
            model_name=result.model_name,
            total_objects=result.total_objects,
            detection_time=result.detection_time,
            boxes=[box.model_dump() for box in result.boxes],
            status="completed",
        )
        db.add(history)
        db.commit()
        db.refresh(history)

        # 将 history_id 附加到结果中
        result_dict = result.model_dump()
        result_dict["detection_id"] = str(history.id)

        return SingleDetectionResponse(
            success=True,
            message="检测成功",
            data=result_dict
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")


@router.get("/targets/list", response_model=TargetListResponse)
async def get_target_list():
    targets = [
        TargetItem(id=0, name="airplane", chinese_name="飞机", description="固定翼飞机、直升机等"),
        TargetItem(id=1, name="oil_tank", chinese_name="油罐", description="储油罐、化工罐等"),
        TargetItem(id=2, name="playground", chinese_name="操场", description="运动场、操场等"),
        TargetItem(id=3, name="building", chinese_name="建筑物", description="各类建筑物"),
        TargetItem(id=4, name="ship", chinese_name="船舶", description="各类船舶"),
        TargetItem(id=5, name="pest", chinese_name="农业虫害", description="农作物病虫害"),
    ]
    return TargetListResponse(
        success=True,
        message="获取成功",
        data=targets
    )
