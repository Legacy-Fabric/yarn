package net.legacyfabric.multifilament.task;

import net.fabricmc.filament.task.base.WithFileOutput;
import net.fabricmc.mappingio.MappingWriter;
import net.fabricmc.mappingio.format.MappingFormat;

import org.gradle.api.file.DirectoryProperty;
import org.gradle.api.provider.Property;
import org.gradle.api.tasks.Input;
import org.gradle.api.tasks.OutputDirectory;
import org.gradle.api.tasks.TaskAction;

import java.io.IOException;

public abstract class MappingOutputTask extends MultiFilamentTask {
	public MappingOutputTask() {
	}

	@Input
	public abstract Property<MappingFormat> getOutputFormat();

	@OutputDirectory
	public abstract DirectoryProperty getOutputDir();

	@TaskAction
	public final void run() throws IOException {
		MappingWriter mappingWriter = MappingWriter.create(this.getOutputDir().getAsFile().get().toPath(), (MappingFormat)this.getOutputFormat().get());

		try {
			this.run(mappingWriter);
		} catch (Throwable var5) {
			if (mappingWriter != null) {
				try {
					mappingWriter.close();
				} catch (Throwable var4) {
					var5.addSuppressed(var4);
				}
			}

			throw var5;
		}

		if (mappingWriter != null) {
			mappingWriter.close();
		}
	}

	abstract void run(MappingWriter var1) throws IOException;
}
